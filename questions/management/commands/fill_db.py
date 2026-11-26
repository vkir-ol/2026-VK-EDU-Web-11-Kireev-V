from itertools import batched
from random import Random
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.test.utils import override_settings
from faker import Faker

from core.models import Profile

from ...models import Answer, AnswerLike, Question, QuestionLike, Tag


BATCH_SIZE = 5000


def insert_in_batches(model, rows):
    for batch in batched(rows, BATCH_SIZE):
        model.objects.bulk_create(batch)


class Command(BaseCommand):
    help = 'Добавляет тестовых пользователей, вопросы, ответы, теги и оценки.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    @override_settings(DEBUG=False)
    @transaction.atomic
    def handle(self, *args, ratio, **options):
        if ratio < 2:
            raise CommandError('ratio должен быть не меньше 2, чтобы оценки не повторялись.')

        fake = Faker('ru_RU')
        rng = Random()
        prefix = uuid4().hex[:10]

        user_ids = self.create_users(fake, prefix, ratio)
        tag_ids = self.create_tags(fake, prefix, ratio)
        question_ids = self.create_questions(fake, rng, user_ids, tag_ids, ratio * 10)

        votes_per_question = min(ratio, 10)
        insert_in_batches(QuestionLike, (
            QuestionLike(
                question_id=question_id,
                user_id=user_id,
                value=rng.choice((1, 1, 1, -1)),
            )
            for question_id in question_ids
            for user_id in rng.sample(user_ids, votes_per_question)
        ))

        answer_count = ratio * 100
        answer_votes = ratio * 200 - len(question_ids) * votes_per_question
        self.create_answers(fake, rng, user_ids, question_ids, answer_count, answer_votes)

        self.stdout.write(self.style.SUCCESS(
            f'Добавлено пользователей: {ratio}, вопросов: {len(question_ids)}, '
            f'ответов: {answer_count}, тегов: {ratio}, оценок: {ratio * 200}.'
        ))

    def create_users(self, fake, prefix, count):
        user_model = get_user_model()
        user_ids = []
        for batch in batched(range(count), BATCH_SIZE):
            users = user_model.objects.bulk_create([
                user_model(
                    username=f'seed_{prefix}_{index}',
                    email=f'seed_{prefix}_{index}@example.com',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password=make_password(None),
                )
                for index in batch
            ])
            Profile.objects.bulk_create([
                Profile(user_id=user.pk, nickname=user.get_full_name()[:30])
                for user in users
            ])
            user_ids.extend(user.pk for user in users)
        return user_ids

    def create_tags(self, fake, prefix, count):
        tag_ids = []
        for batch in batched(range(count), BATCH_SIZE):
            tags = Tag.objects.bulk_create([
                Tag(name=f'{fake.word()[:12]}-{prefix}-{index}')
                for index in batch
            ])
            tag_ids.extend(tag.pk for tag in tags)
        return tag_ids

    def create_questions(self, fake, rng, user_ids, tag_ids, count):
        question_ids = []
        tag_relation = Question.tags.through
        tag_count = min(3, len(tag_ids))
        for batch in batched(range(count), BATCH_SIZE):
            questions = Question.objects.bulk_create([
                Question(
                    author_id=rng.choice(user_ids),
                    title=f'{fake.sentence(nb_words=7).rstrip(".")[:119]}?',
                    text=fake.paragraph(nb_sentences=3),
                )
                for _ in batch
            ])
            insert_in_batches(tag_relation, (
                tag_relation(question_id=question.pk, tag_id=tag_id)
                for question in questions
                for tag_id in rng.sample(tag_ids, tag_count)
            ))
            question_ids.extend(question.pk for question in questions)
        return question_ids

    def create_answers(self, fake, rng, user_ids, question_ids, count, total_votes):
        answer_texts = [fake.paragraph(nb_sentences=3) for _ in range(4096)]
        votes_per_answer, extra_votes = divmod(total_votes, count)

        for batch in batched(range(count), BATCH_SIZE):
            answers = Answer.objects.bulk_create([
                Answer(
                    question_id=question_ids[index % len(question_ids)],
                    author_id=rng.choice(user_ids),
                    text=rng.choice(answer_texts),
                    is_correct=index < len(question_ids) and rng.random() < 0.3,
                )
                for index in batch
            ])
            insert_in_batches(AnswerLike, (
                AnswerLike(
                    answer_id=answer.pk,
                    user_id=user_id,
                    value=rng.choice((1, 1, 1, -1)),
                )
                for index, answer in zip(batch, answers)
                for user_id in rng.sample(user_ids, votes_per_answer + (index < extra_votes))
            ))