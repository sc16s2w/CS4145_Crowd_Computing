import json

def parsing_toloka(path):
    tasks = {}
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if 'left' not in line:
                continue
            box_list = []
            items = line.split('\t')
            url = items[0].strip()
            box = items[2].replace('\"','').replace('{','').replace('}','').replace('\\','')
            ps = box.split('shape:rectangle,')
            for p in ps:
                if 'left' not in p:
                    continue
                p = p.replace('left:','').replace('top:','').replace('width:','').replace('height:','').replace('label:','')
                p1 = p.split(',')

                top = float(p1[1])
                left = float(p1[0])
                bottom = top - float(p1[3])
                right = left + float(p1[2])

                box = [top, left, bottom, right]
                box_list.append(box)
            if url not in tasks.keys():
                tasks[url] = []
            tasks[url].append(box_list)

    return tasks


def parseing_box(box):
    box_list = []

    box = box.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','').replace('type:rectangle,data:p1:','')

    for i in range(1,8):
        r = ',annotation:Entity {},'.format(i)
        box = box.replace(r,',')
    box = box.replace(',annotation:Entity 8', '').replace(',p2:',',').replace('x:','').replace('y:','')
    #print(box)

    coordinates = box.split(',')

    for i in range(len(coordinates)//4):
        x1 = float(coordinates[i*4])
        y1 = float(coordinates[i*4 + 1])
        x2 = float(coordinates[i*4 + 2])
        y2 = float(coordinates[i*4 + 3])
        left = min(x1,x2)
        right = max(x1,x2)
        top = max(y1,y2)
        bottom = min(y1,y2)
        box_list.append([top, left, bottom, right])
    return box_list


def parsing_improved(path):
    tasks = {}
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if 'rectangle' not in line:
                continue

            items = line.split('\t')
            url = items[0].strip()
            box = items[10]

            test = url.split('19.j')
            if len(test) > 1:
                pass
            else:
                pass

            if url not in tasks.keys():
                tasks[url] = []

            tasks[url].append(parseing_box(box))

    return tasks

def iou(box1, box2):
    '''
    两个框（二维）的 iou 计算

    注意：边框以左上为原点

    box:[top, left, bottom, right]
    '''
    in_h = min(box1[0], box2[0]) - max(box1[2], box2[2])
    in_w = min(box1[3], box2[3]) - max(box1[1], box2[1])
    inter = 0 if in_h < 0 and in_w < 0 else in_h * in_w
    union = (box1[0] - box1[2]) * (box1[3] - box1[1]) + \
            (box2[0] - box2[2]) * (box2[3] - box2[1]) - inter
    iou = inter / union
    return iou

def iou_batch(groud_truth_map, box_map):
    res = {}
    for url in box_map:
        truth_boxes = groud_truth_map[url][0]
        answer_boxes = box_map[url]

        for answer_box in answer_boxes:
            total_iou = 0.0
            for box in answer_box:
                max_iou_tmp = 0.0
                for box_true in truth_boxes:
                    i = iou(box_true, box)
                    if i > max_iou_tmp:
                        max_iou_tmp = i
                total_iou += max_iou_tmp

            if url not in res.keys():
                res[url] = []
            res[url].append([total_iou/len(answer_box), total_iou/len(truth_boxes)])

    return res

# def iou_batch(groud_truth_map, box_map):
#     res = []
#     for box in box_map:
#         max_iou_tmp = 0.0
#         for box_true in groud_truth_map:
#             i = iou(box_true, box)
#             if i > max_iou_tmp:
#                 max_iou_tmp = i
#         res.append(max_iou_tmp)
#
#     return res


def writeTSV(path, accuracies):
    with open(path, 'w+') as write_tsv:
        line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('picId', 'accuracy11', 'accuracy12', 'accuracy21', 'accuracy22', 'accuracy31', 'accuracy32', 'average')
        write_tsv.write(line)
        for url in accuracies:
            key = url.replace('https://raw.githubusercontent.com/sc16s2w/CS4145_Crowd_Computing/main/', '')
            key = int(key.replace('.jpg', ''))
            acc = accuracies[url]
            avg = (acc[0][0] + acc[1][0] + acc[2][0])/3
            line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(key, acc[0][0], acc[0][1], acc[1][0], acc[1][1], acc[2][0], acc[2][1], avg)
            write_tsv.write(line)

if __name__ == '__main__':
    truth_box_map = parsing_toloka('GroundTruth.tsv')

    # # Baseline start
    # baseline_box_map = parsing_toloka('baseline.tsv')
    # accuracies_baseline = iou_batch(truth_box_map, baseline_box_map)
    # writeTSV('result_baseline.tsv', accuracies_baseline)
    # # Baseline end
    #
    # # Improved start
    # improved_box_map = parsing_improved('improved.tsv')
    # accuracies_improved = iou_batch(truth_box_map, improved_box_map)
    # writeTSV('result_improved.tsv', accuracies_improved)
    # # Improved end

    # Baseline train start
    baseline_box_map = parsing_toloka('baseline_train_answer.tsv')
    accuracies_baseline = iou_batch(truth_box_map, baseline_box_map)
    writeTSV('result_baseline_train.tsv', accuracies_baseline)
    # Baseline train end

    # Improved train start
    improved_box_map = parsing_improved('improved_train_answer.tsv')
    accuracies_improved = iou_batch(truth_box_map, improved_box_map)
    writeTSV('result_improved_train.tsv', accuracies_improved)
    # Improved train end
