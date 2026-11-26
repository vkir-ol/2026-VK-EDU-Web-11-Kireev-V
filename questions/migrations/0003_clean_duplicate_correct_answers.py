from django.db import migrations
from django.db.models import Min

def clean_duplicate_correct_answers(apps, schema_editor):
    Answer = apps.get_model('questions', 'Answer')
    correct = Answer.objects.using(schema_editor.connection.alias).filter(is_correct=True)

    keep_ids = (
        correct.order_by()
        .values('question_id')
        .annotate(keep_id=Min('pk'))
        .values('keep_id')
    )
    correct.exclude(pk__in=keep_ids).update(is_correct=False)

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_rating_from_votes'),
    ]

    operations = [
         migrations.RunPython(
            clean_duplicate_correct_answers,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
