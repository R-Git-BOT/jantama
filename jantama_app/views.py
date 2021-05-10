
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

from datetime import datetime as dt
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm

from jantama_app.models import User,Match

# ユーザー作成
def create_user(request):
    """
    create new user data
    """
    post = User()

    if request.method == 'GET':
        # 新規作成オブジェクトにより form を作成
        form = PostUserForm(instance=post)

        # ページロード時は form を Template に渡す
        return render(request,
                        'jantama_app/create_user.html',  # 呼び出す Template
                        {'form': form})  # Template に渡すデータ
    
    # 実行ボタン押下時
    if request.method == 'POST':
        # POST されたデータにより form を作成
        form = PostUserForm(request.POST, instance=post)

        post = form.save(commit=False)
        post.save()

        return redirect('jantama_app:create_match_post')

# 試合データ作成
def create_match_post(request):
    """
    cureate new match data
    """
    
    post = Match()

    if request.method == 'GET':
        # 新規作成オブジェクトにより form を作成
        form = PostMatchForm(instance=post)

        # ページロード時は form を Template に渡す
        return render(request,
                        'jantama_app/post_match_form.html',  # 呼び出す Template
                        {'form': form})  # Template に渡すデータ
    
    # 実行ボタン押下時
    if request.method == 'POST':
        # POST されたデータにより form を作成
        form = PostMatchForm(request.POST, instance=post)

        post = form.save(commit=False)
        post.save()

        return redirect('jantama_app:read_post')

# 試合データ一覧
def read_post(request):
    """
    データの一覧を表示する
    """
    # 全試合結果オブジェクトを取得
    posts = Match.objects.all().order_by('id')
    return render(request,
                    'jantama_app/match_list.html',  # 呼び出す Template
                    {'posts': posts})  # Template に渡すデータ

# 試合データ編集
def edit_match_post(request, post_id):
    """
    対象のデータを編集する
    """
    # IDを引数に、対象オブジェクトを取得
    post = get_object_or_404(Match, pk=post_id)

    # ページロード時
    if request.method == 'GET':
        # 対象オブジェクトにより form を作成
        form = PostMatchForm(instance=post)

        # ページロード時は form とデータIDを Template に渡す
        return render(request,
                        'jantama_app/post_match_form.html',  # 呼び出す Template
                        {'form': form, 'post_id': post_id})  # Template に渡すデータ

    # 実行ボタン押下時
    elif request.method == 'POST':
        # POST されたデータにより form を作成
        form = PostMatchForm(request.POST, instance=post)

        post = form.save(commit=False)
        post.save()

        # 実行ボタン押下時は処理実行後、一覧画面にリダイレクトする
        return redirect('jantama_app:read_post')

# 試合データ削除
def delete_match_post(request, post_id):
    # 対象のオブジェクトを取得
    post = get_object_or_404(Match, pk=post_id)
    post.delete()

    # 削除リクエスト時は削除実行後、一覧表示画面へリダイレクトする
    return redirect('jantama_app:read_post')


# 試合による累計ランクポイントをグラフで表示する
def match_graph(request):
    data = []
    label = []

    queryset = Match.objects.order_by('id')
    for total in queryset:
        data.append(total.total_point)
        label.append((total.mdate).strftime('%Y-%m-%d %H:%M:%S'))   #文字列にしないとグラフが表示されない！！！
    print(data)
    print(label)

    return render(request, 'jantama_app/match_graph.html', {
        'data': data,
        'label': label,
    })

class PostUserForm(ModelForm):
    """
    ユーザー登録するフォーム
    """
    class Meta:
        model = User
        # fields は models.py で定義している変数名
        fields = ('name', 'now_dan', 'now_rank_point')

class PostMatchForm(ModelForm):
    """
    試合結果を登録するフォーム
    """
    class Meta:
        model = Match
        fields = ('name', 'half', 'taku', 'mdate', 'rank', 'result_point')