"""
某班有6名学生，

   1）输入该班每个学生的成绩
   2）计算并输出该班的总分和平均分
   3）输出该班学生的最高分和最低分及其相应的下标
   4）输入一个成绩，查看该班有没有该成绩

"""

# 1）输入该班每个学生的成绩
scores_str = input('请输入各学生成绩，以逗号隔开：')
scores_temp = scores_str.split(",")

scores = [float(i) for i in scores_temp]

# 2）计算并输出该班的总分和平均分
sum_score = 0
for score in scores:
    sum_score += float(score)
print('总分: %f, 平均成绩: %f' % (sum_score, sum_score / scores.__len__()))

# 3）输出该班学生的最高分和最低分及其相应的下标

scores_sort = array(scores)
length = len(scores_sort)
while length > 0:
    for i in range(length - 1):
        if scores_sort[i] > scores_sort[i + 1]:
            scores_sort[i] = scores_sort[i] + scores_sort[i + 1]
            scores_sort[i + 1] = scores_sort[i] - scores_sort[i + 1]
            scores_sort[i] = scores_sort[i] - scores_sort[i + 1]
    length -= 1
print(scores_sort)
print(scores)
max = scores_sort[scores_sort.__len__() - 1]
min = scores_sort[0]
print('最高分: %2.f 下标: %d, 最低分: %.2f 下标: %d' % (max, scores.index(max), min, scores.index(min)))
