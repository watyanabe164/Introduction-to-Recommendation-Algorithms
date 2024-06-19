from dataset import dataset
from similarity import get_similairty

def get_recommend(person, top_N):

  totals = {} ; simSums = {} #推薦度スコアを入れるための箱を作っておく

  # 自分以外のユーザのリストを取得してFor文を回す
  # -> 各人との類似度、及び各人からの（まだ本人が見てない）映画の推薦スコアを計算するため
  list_others = list(dataset.keys()) ; list_others.remove(person)

  for other in list_others:
    # 本人がまだ見たことが無い映画の集合を取得
    set_other = set(dataset[other]); set_person = set(dataset[person])
    set_new_movie = set_other.difference(set_person)

    # あるユーザと本人の類似度を計算(simは0~1の数字)
    sim = get_similairty(person, other)

    # (本人がまだ見たことがない)映画のリストでFor分を回す
    for item in set_new_movie:

      # "類似度 x レビュー点数" を推薦度のスコアとして、全ユーザで積算する
      totals.setdefault(item,0)
      totals[item] += dataset[other][item]*sim 

      # またユーザの類似度の積算値をとっておき、これで上記のスコアを除する
      simSums.setdefault(item,0)
      simSums[item] += sim

  rankings = [(total/simSums[item],item) for item,total in totals.items()]
  rankings.sort()
  rankings.reverse()

  return [i[1] for i in rankings][:top_N]
