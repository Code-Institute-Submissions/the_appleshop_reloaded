from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Review
from django.contrib.auth.models import User
from products.models import Product
from .forms import ReviewForm
from django.utils import timezone
from django.contrib import messages
from products.views import get_user_purchases


def get_reviews(request):
    """
    Creates view with overview of entered reviews prior to 'now'
    """
    reviews = Review.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, "reviews.html",
                  {'reviews': reviews, "testvalue": 99})


def review_detail(request, pk):
    """
    Create a view that returns a single
    Review object based on the post ID (id) and
    render it to the 'reviewdetail.html' template.
    Or return a 404 error if the review is
    not found
    """
    review = get_object_or_404(Review, pk=pk)
    review.view_count += 1
    review.save()
    return render(request, "reviewdetail.html", {'review': review})


def create_review(request, pk):
    """
    Create a view that allows us to create
    or edit a review depending if the Review ID
    is null or not
    """
    product = Product.objects.get(pk=pk)
    purchased_products = get_user_purchases(request.user)
    if request.user.is_authenticated and product.name in purchased_products:
        review = Review(author=request.user, product=product)
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.author.id = request.user.id
                review.product.pk = pk
                review.name = product.name
                print(product)
                product.review_count+=1
                product.save
                review.save()
                return redirect(review_detail, review.pk)
        else:
            form = ReviewForm(instance=review)

        return render(request, 'editform.html', {'form': form})
    else:
        return redirect(reverse('get_reviews'))


def edit_review(request, pk):
    """
    Create a view that allows us to create
    or edit a review depending if the Review ID
    is null or not
    """
    review = get_object_or_404(Review, pk=pk) if pk else None
    if request.user.is_authenticated and review.author.id == request.user.id:
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                return redirect(review_detail, review.pk)
        else:
            form = ReviewForm(instance=review)

        return render(request, 'editform.html', {'form': form})

    else:
        return redirect(reverse('get_reviews'))


def delete_review(request, pk):
    """
    View for deleting a review, requested by author
    """
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_authenticated and review.author.id == request.user.id:
        if request.method == "GET":
            review.delete()
            messages.success(request, "Review has been deleted")
            return redirect(reverse('get_reviews'))
    else:
        return redirect(reverse('get_reviews'))
