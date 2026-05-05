import copy
import sys

sys.setrecursionlimit(2000)

N= int(input())
check = [0 for _ in range(N)]
visit = [0 for _ in range(N)]
Matrix = []
MST_node = []
MST_node_weight = []
MST = []
MST_copy = []
MST_weight = []
travel_route = []

def mst(node):
    check[node] = 1

    if 0 not in check:
        return 0

    for i in range(N):
        if check[i] != 1:
            MST_node.append([node, i])
            MST_node_weight.append(Matrix[node][i])

    mwi = MST_node_weight.index(min(MST_node_weight))
    MST.append(MST_node[mwi]) #MST에 가장 짧은 간선 추가
    MST_weight.append(MST_node_weight[mwi]) #MST 간선에 부여된 가중치 추가
    temp = MST_node.pop(mwi)
    del MST_node_weight[mwi]
    mst(temp[1])


def travel(vil):
    visit[vil] = 1 #방문한 마을 체크
    travel_route.append(vil) # 방문한 장소 루트에 추가하기

    if 0 not in visit: #모든곳을 방문했다면 처음마을로 복귀하고 종료
        travel_route.append(0)
        return 0

    MinCost = max(MST_weight) #최소 비용

    if 0 not in visit: #모든곳을 방문했다면 처음마을로 복귀하고 종료
        travel_route.append(0)
        return 0

    connected_nodes = [x for x in MST_copy if x[0] == vil] #현재 있는 마을과 연결된 마을의 리스트
    if not connected_nodes: #연결된 마을이 없으면
        for node in MST_copy:
            if MinCost > MST_weight[MST_copy.index(node)]:
                MinCost = MST_weight[MST_copy.index(node)]
        temp = MST_copy.pop(MST_weight.index(MinCost))
        del MST_weight[MST_weight.index(MinCost)]
        travel(temp[1])
    else: #연결된 마을이 있으면
        for node in MST_copy:
            if node[0] == vil:
                if MinCost > MST_weight[MST_copy.index(node)]:
                    MinCost = MST_weight[MST_copy.index(node)]
        temp = MST_copy.pop(MST_weight.index(MinCost))
        del MST_weight[MST_weight.index(MinCost)]
        travel(temp[1])


for i in range(N):
    Matrix.append(list(map(int,input().split())))

mst(0)
MST_copy = copy.deepcopy(MST)
travel(0)

print("MST:",end=" ")
for i in MST:
    print(f'({i[0]}, {i[1]})',end=" ")
print()
print("방문 경로:",end=" ")
for i in travel_route:
    print(i,end=" ")
