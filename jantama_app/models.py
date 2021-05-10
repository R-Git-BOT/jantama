import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    
    name = models.CharField('user name', max_length=10, default='imput name')
    now_dan = models.CharField('now dan-i', max_length=10, default='shi1')  # 現在の段位
    now_rank_point = models.IntegerField('now dan-i point') # 現在のランクポイント
    now_total_point = models.IntegerField('now Total point')    # 現在の累計ポイント

    def __str__(self):
        return self.name

    def get_rank_point(self):
        
        # 特定ランク（Key）になるまでの累計ポイント(Value)
        dict_rank_point = {"shin1":0,"shin2":20,"shin3":100,"shi1":300,"shi2":900,"shi3":1700
                ,"ketsu1":2700,"ketsu2":3900,"ketsu3":5300,"go1":7300,"go2":10100,"go3":13300
                ,"sei1":16900,"sei2":20900,"sei3":26900,"ten":35900}

        # 現在の累計ポイントは現在ランクに到達するまでの累計ポイントと今現在のランクポイントの合計で算出
        now_total_point = dict_rank_point[self.now_dan]     
        return now_total_point + self.now_rank_point
    
    def save(self, *args, **kwargs):    
        self.now_total_point = self.get_rank_point()
        super().save(*args, **kwargs)



class Match(models.Model):
    name = models.CharField('user name',max_length=10, default='sample')    # なまえ
    half = models.BooleanField(default=False)                           # 半荘か東風か True=半荘
    taku = models.CharField('taku', max_length=10, default='silver')    # プレイした卓 これによって色々変動
    mdate = models.DateTimeField('match date',default=timezone.now)     # プレイした日 面倒なのでデフォルトを今の時間に
    dan = models.CharField('now danni', max_length=10, default='shi1')  # プレイした時の段位
    rank = models.IntegerField('match rank') # junni                    # 順位
    result_point = models.IntegerField('result point')                  # 修了時の点数
    rank_point = models.IntegerField('rank point')                      # ランクポイントの増減
    total_point = models.IntegerField('total point')                    # nameの累計ポイント

    def __str__(self):
        return str(self.mdate)

    def get_pmpoint(self):
        res_point = round((self.result_point - 25000) / 1000)   # 25000点持ち25000点返し 素点に変える
        
        # 4位の場合に惹かれる点数 Key：段位 Value：引かれる点数 tは東風 hは半荘
        dict_rank4_t = {"shin1":-15,"shin2":-15,"shin3":-15,"shi1":-25,"shi2":-35,"shi3":-45
                ,"ketsu1":-55,"ketsu2":-65,"ketsu3":-75,"go1":-95,"go2":-105,"go3":-115
                ,"sei1":-125,"sei2":-135,"sei3":-135,"ten":-155}
        dict_rank4_h = {"shin1":-15,"shin2":-15,"shin3":-15,"shi1":-35,"shi2":-55,"shi3":-75
                ,"ketsu1":-95,"ketsu2":-115,"ketsu3":-135,"go1":-180,"go2":-195,"go3":-210
                ,"sei1":-225,"sei2":-240,"sei3":-255,"ten":-270}

        # 1位の場合に足される点数 Key：卓 Value：点数
        dict_taku_rank1_t = {"bronze":25,"silver":35,"gold":55,"gyoku":70,"ouza":75}
        dict_taku_rank1_h = {"bronze":35,"silver":55,"gold":95,"gyoku":125,"ouza":135}
        
        # 2位の場合に足される点数 上に同じ
        dict_taku_rank2_t = {"bronze":10,"silver":15,"gold":25,"gyoku":35,"ouza":35}
        dict_taku_rank2_h = {"bronze":15,"silver":25,"gold":45,"gyoku":60,"ouza":65}
        
        if self.rank == 3:  # 3位の場合は-5点で固定
            return res_point - 5
        elif self.rank == 1:
            if self.half:
                return res_point + dict_taku_rank1_h[self.taku]
            else:
                return res_point + dict_taku_rank1_t[self.taku]
        elif self.rank == 2:
            if self.half:
                return res_point + dict_taku_rank2_h[self.taku]
            else:
                return res_point + dict_taku_rank2_t[self.taku]
        elif self.rank == 4:
            if self.half:
                return res_point + dict_rank4_h[self.dan]
            else:
                return res_point + dict_rank4_t[self.dan]

    def get_total_point(self):  # 今現在のuserの累計ポイントを試合データの増減ポイントから計測
        user = User.objects.get(name=self.name)

        user.now_rank_point = user.now_rank_point + self.rank_point
        user.save()
        return user.now_rank_point

    def get_danni(self):        # 今現在のuserの段位を取得
        user = User.objects.get(name=self.name)
        return user.now_dan

    def danni_check(self):      # userが昇段したかチェック
        user = User.objects.get(name=self.name)

        # 次の段位に必要な点数
        danni_next = {"shin1":20,"shin2":80,"shin3":200,"shi1":600,"shi2":800,"shi3":1000
                ,"ketsu1":1200,"ketsu2":1400,"ketsu3":2000,"go1":2800,"go2":3200,"go3":3600
                ,"sei1":4000,"sei2":6000,"sei3":9000}
        
        # 昇段時に最初からもらえる点数 昇段時初期ポイント
        danni_kiso = {"shin1":0,"shin2":0,"shin3":0,"shi1":300,"shi2":400,"shi3":500
                ,"ketsu1":600,"ketsu2":700,"ketsu3":1000,"go1":1400,"go2":1600,"go3":1800
                ,"sei1":2000,"sei2":3000,"sei3":45000,"ten":10000}

        # 段位のリスト
        danni = ["shin1","shin2","shin3","shi1","shi2","shi3","ketsu1","ketsu2","ketsu3",
                "go1","go2","go3","sei1","sei2","sei3","ten"]

        # もし段位が上がっていたら、userの段位を1上げて累計ポイントに昇段時初期ポイントを加算
        if user.now_rank_point > danni_next[user.now_dan]:
            index = danni.index(user.now_dan)
            user.now_dan = danni[index+1]
            user.save()
            print(user.now_dan)
            user.now_total_point = user.now_total_point + danni_kiso[user.now_dan]
            user.save()

        return 

    def save(self, *args, **kwargs):
        self.dan = self.get_danni()
        self.rank_point = self.get_pmpoint()
        self.total_point = self.get_total_point()

        # 初心は段位ポイントが0未満にならない
        if self.dan == 'shi1' or self.dan == 'shi2' or self.dan == 'shi3':
            if self.total_point < 0:
                self.total_point = 0

        self.danni_check()
        
        super().save(*args, **kwargs)