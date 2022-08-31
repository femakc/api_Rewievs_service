# Generated by Django 2.2.16 on 2022-08-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Текст отзыва')),
                ('score', models.SmallIntegerField(choices=[(1, '1. Очень плохо. Не понравилось совсем.'), (2, '2. Плохо. Не понравилось почти всё.'), (3, '3. Не очень. Не понравилось многое.'), (4, '4. Так себе. Мало что понравилось.'), (5, '5. Ни то, ни сё. Почти ничего не понравилось.'), (6, '6. Неплохо. Кое-что понравилось.'), (7, '7. Хорошо. Многое понравилось.'), (8, '8. Очень хорошо. Почти всё понравилось.'), (9, '9. Великолепно. Очень понравилось.'), (10, '10. Высший балл. В восторге.')], verbose_name='Рейтинг')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отзыва')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('year', models.IntegerField(default=2000)),
                ('description', models.TextField(default='')),
            ],
        ),
    ]
