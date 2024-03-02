from educational.similarity import taskTheta
from educational.constructions import CONSTRUCTIONS
from tskmanager import Task
from config import HOWMANYHINTS

def getScore(num):
    return taskTheta(Task.Instance(), CONSTRUCTIONS[num][0])

def formRecommends():
    answer = ''
    for j, ind in enumerate(sorted(list(CONSTRUCTIONS.keys())[:HOWMANYHINTS], key=lambda n: getScore(n))):
        answer += f'{j+1}) {CONSTRUCTIONS[ind][1]} \n <br>'
    return answer

