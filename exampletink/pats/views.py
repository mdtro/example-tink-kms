import base64

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserGitHubToken
from .forms import GitHubTokenForm


@login_required
def save_token(request):
    if request.method == "POST":
        form = GitHubTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]
            user_token = UserGitHubToken.objects.create(user=request.user)
            user_token.set_token(token)
            user_token.save()
            return redirect("success")
    else:
        form = GitHubTokenForm()

    return render(request, "pats/save_token.html", {"form": form})


@login_required
def success(request):
    return render(request, "pats/success.html")


@login_required
def view_tokens(request):
    # Fetch all GitHub tokens for the current user
    user_tokens = UserGitHubToken.objects.filter(user=request.user)

    # Prepare tokens with decrypted and Base64 encoded values
    tokens_data = []
    for token in user_tokens:
        decrypted_token = token.get_token()
        encrypted_token_base64 = base64.b64encode(token.encrypted_token).decode("utf-8")
        tokens_data.append({
            "id": token.id,
            "encrypted_token_base64": encrypted_token_base64,
            "decrypted_token": decrypted_token,
        })

    return render(
        request,
        "pats/view_tokens.html",
        {
            "tokens_data": tokens_data,
        },
    )
