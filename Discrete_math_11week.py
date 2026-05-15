import heapq
from heapq import heappop,heappush

n,q = map(int, input().split())

tree = []
pq = []
preorder_Arr = []

q_Arr = []

wList = list(map(int,input().split())) #노드(로그) 별 가중치(빈도) 저장

for i in range(q):
    q_Arr.append(input().split())

#3번 질의 같은 경우 bit 형식으로 데이터로 저장되어있기 때문에 따로 분류함
for i in range(q):
    if q_Arr[i][0] != '3':
        q_Arr[i] = list(map(int,q_Arr[i]))
    else:
        q_Arr[i][0] = int(q_Arr[i][0])

#트리 생성 전 처음 로그 배열로 저장
for i in range(n):
    weight = wList[i]
    minIndex = i + 1
    Id = i + 1
    left = -1
    right = -1
    heappush(pq,(weight,minIndex,Id,left,right))
    tree.append((weight,minIndex,Id,left,right)) #tree는 Id 순서대로 배치해야하므로 따로 할당

#트리 생성
e = n + 1
while len(pq) > 1:
    e1 = heappop(pq)
    e2 = heappop(pq)

    heappush(pq,(e1[0] + e2[0],min(e1[1],e2[1]),e,e1[2],e2[2]))
    tree.append((e1[0] + e2[0],min(e1[1],e2[1]),e,e1[2],e2[2]))

    e += 1 #id 1씩 늘려가면서 내부노드 id 배정

#부모노드 방문 체크 지우고 다시 부모노드로 돌아가서

def preorder(order):
    #내부노드인지 기존노드인지 확인 후 출력
    if tree[order][2] < n + 1:
        preorder_Arr.append(tree[order][2]) # 전위 순회 배열에 저장
    else:
        preorder_Arr.append('#') #전위 순회 배열에 저장(내부노드는 #으로 저장

    #트리 전위순회 (3은 left, 4는 right임. 그 뒤에 5과 6은 각각 깊이와 허프만 코드)
    if tree[order][3] != -1 :
        tree[tree[order][3] - 1] = tree[tree[order][3] - 1] + (tree[order][5] + 1,) #트리 높이 저장
        tree[tree[order][4] - 1] = tree[tree[order][4] - 1] + (tree[order][5] + 1,)

        tree[tree[order][3] - 1] = tree[tree[order][3] - 1] + (tree[order][6] + '0',)
        tree[tree[order][4] - 1] = tree[tree[order][4] - 1] + (tree[order][6] + '1',)

        #print("결과",tree[tree[order][3] - 1], sep=':')
        preorder(tree[order][3] - 1) # left 먼저 (-1 붙인이유는 순서에 +1 해서 저장했으니까)
        preorder(tree[order][4] - 1) # right 는 나중에

def treeDepth():
    temp = []
    for i in tree:
        temp.append(i[5])
    maxdepth = max(temp) #모든 깊이 중 가장 큰 깊이 저장
    return maxdepth

def calculateBit():
    Sum = 0
    for i in range(n):
        Sum += tree[i][0] * len(tree[i][6])
    return Sum

def decode(s,node):
    #리프노드에 도달할 경우
    if tree[node][3] == -1:
        return tree[node][2]

    if q_Arr[s][1][0] == '0':
        q_Arr[s][1] = q_Arr[s][1][1:]
        return decode(i,tree[node][3] - 1)
    elif q_Arr[s][1][0] == '1':
        q_Arr[s][1] = q_Arr[s][1][1:]
        return decode(s,tree[node][4] - 1)
    else:
        return 0


tree[-1] = tree[-1] + (0,) #루트 노드 깊이 저장
tree[-1] = tree[-1] + ('',) #루트 노드 허프만 코드(재귀 넘겨받기용)
preorder(-1) #tree(pq)의 마지막에 루트 노드가 있으므로 -1로 호출

print(treeDepth(),end=' ') #트리 높이 출력

print(calculateBit()) #노드별 허프만비트 저장

print(*preorder_Arr,sep=' ') #전위순회 결과 저장

#질의 답 구하기
for i in range(q):
    #1번 질의일 경우
    if q_Arr[i][0] == 1:
        print(tree[q_Arr[i][1]-1][6]) #허프만 코드 출력 q_Arr[i][1] - 1은 질의에서 주어진 로그값임.
    #2번 질의일 경우
    elif q_Arr[i][0] == 2:
        Sum = 0
        for j in range(2,q_Arr[i][1]+2):
            Sum += len(tree[q_Arr[i][j]-1][6])
        print(Sum)
    #3번 질의일 경우
    elif q_Arr[i][0] == 3:
        q_Arr[i][1] = str(q_Arr[i][1])
        temp = []
        while len(q_Arr[i][1]) > 0:
            temp.append(decode(i,-1))
        print(*temp,sep=' ')

