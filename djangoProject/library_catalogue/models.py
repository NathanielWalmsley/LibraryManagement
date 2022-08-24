from django.db import models

class LibraryBranch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Borrower(models.Model):
    card_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    models.UniqueConstraint(
        fields=[title, publisher],
        name='unique_title_publisher_constraint'
    )

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
    stock = models.IntegerField()
    models.UniqueConstraint(
        fields=[book_id, branch_id],
        name='unique_book_and_branch_constraint'
    )


class Loan(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
    card_number = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    date_out = models.DateField('date loaned')
    date_due = models.DateField('date due for return')