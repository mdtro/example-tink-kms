from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserGitHubToken
from .forms import GitHubTokenForm


@login_required
def save_token(request):
    if request.method == "POST":
        form = GitHubTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]
            user_token, created = UserGitHubToken.objects.get_or_create(
                user=request.user
            )
            user_token.set_token(token)
            user_token.save()
            return redirect("success")
    else:
        form = GitHubTokenForm()

    return render(request, "github_tokens/save_token.html", {"form": form})
