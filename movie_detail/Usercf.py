import math


class Usercf:
    def __init__(self,data):
        self.data=data
    # 计算2个用户的相似度 ：欧式距离公式
    def  Euclidean(self,user1,user2):
         data1=self.data[user1]
         data2=self.data[user2]
         xiangshidu=0
         for moiveid,score in data1.items():
             if moiveid in data2.keys():
                   xiangshidu+=math.pow(float(score)-float(data2[moiveid]),2)

         return 1/(1+math.sqrt(xiangshidu))
    # 计算登录的用户与数据库的用户相似度
    def  top_simliar(self,userID):
         user_message=[]
         for userid  in self.data.keys():
              if userid == float(userID):
                  continue
              else:
                  xiansdu=self.Euclidean(float(userID),userid)

                  user_message.append((userid,xiansdu))
         user_message.sort(key=lambda val:val[1],reverse=True)
         return user_message
    # 找最高相似度的用户的评价电影记录来推荐，并去掉同时都观看过的
    def recommend(self,user):
           tjmoive=[]
           top_one=self.top_simliar(user)
           if top_one != []:
               top_one=top_one[0][0]
               watch_moive=self.data[top_one]
               for moive_id,score in watch_moive.items():
                   if not moive_id in self.data[float(user)].keys():
                       tjmoive.append((moive_id,score))
               tjmoive.sort(key=lambda val: val[1], reverse=True)
               return  tjmoive
           else:
               return  top_one