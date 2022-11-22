import math


class itemcf():
    def __init__(self,data):
         self.data=data
    def Euclidean(self,item1,item2):
        item1_info=self.data[float(item1)]
        item2_info = self.data[item2]
        xiangshidufenzhi= 0
        xiangshidufenmuqian=0
        xiangshidufenmuhou=0
        for userid in item1_info.keys():
             xiangshidufenmuqian+=math.pow(item1_info[userid],2)
             if userid in item2_info.keys():
                 xiangshidufenzhi+=item1_info[userid]*item2_info[userid]
        for userid2 in item2_info.keys():
            xiangshidufenmuhou+=math.pow(item2_info[userid2],2)
        xiangshidufenmu=xiangshidufenmuqian*xiangshidufenmuhou
        return xiangshidufenzhi/math.sqrt(xiangshidufenmu)
    def top_simliar(self, itemID):
        item_message = []
        for itemid in  self.data.keys():
            if itemid == float(itemID):
                continue
            else:
                xianshidu=self.Euclidean(itemID,itemid)
                item_message.append((itemid,xianshidu))
        item_message.sort(key=lambda val:val[1],reverse=True)
        print(item_message)
        return  item_message
