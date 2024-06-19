from dataset import dataset
from math import sqrt

def get_similairty(person1, person2):

  ## 両者とも見た映画の集合を取る
  set_person1 = set(dataset[person1].keys())
  set_person2 = set(dataset[person2].keys())
  set_both = set_person1.intersection(set_person2)

  if len(set_both)==0: #共通でみた映画がない場合は類似度を0とする
    return 0

  list_destance = []

  for item in set_both:
    # 同じ映画のレビュー点の差の2乗を計算
    # この数値が大きいほど「気が合わない」=「似ていない」と定義できる 
    distance = pow(dataset[person1][item]-dataset[person2][item], 2) 
    list_destance.append(distance)

  return 1/(1+sqrt(sum(list_destance))) #各映画の気の合わなさの合計の逆比的な指標を返す
