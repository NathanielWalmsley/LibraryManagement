# Generated by Django 4.1 on 2022-08-23 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('card_number', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_out', models.DateField(verbose_name='date loaned')),
                ('date_due', models.DateField(verbose_name='date due for return')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.book')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.librarybranch')),
                ('card_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.borrower')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.book')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.librarybranch')),
            ],
        ),
        migrations.CreateModel(
            name='BookAuthorLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.author')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_catalogue.book')),
            ],
        ),
    ]
