from django.db import migrations


def move_event_choices_to_choice_model(apps, schema_editor):
    Event = apps.get_model("vote", "Event")
    Choice = apps.get_model("vote", "Choice")
    for event in Event.objects.all():
        for choice in event.choices:
            new_choice = Choice(label=choice, alias=None, event=event)
            new_choice.save()

            event.choices = ""
            event.save()


def reverse_move_event_choices_to_choice_model(apps, schema_editor):
    Event = apps.get_model("vote", "Event")
    for event in Event.objects.all():
        new_choices = []
        for choice in event.choice_set.all():
            new_choices.append(choice.label)
            choice.delete()

        event.choices = new_choices
        event.save()


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("vote", "0013_choice"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(
            move_event_choices_to_choice_model,
            reverse_code=reverse_move_event_choices_to_choice_model,
        )
    ]
