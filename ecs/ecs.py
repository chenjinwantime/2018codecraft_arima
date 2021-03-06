# coding=utf-8
import sys
import os
import predictor


def main():
    print 'main function begin.'
    if len(sys.argv) != 4:
        print 'parameter is incorrect!'
        print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
        exit(1)
    # Read the input files
    ecsDataPath = sys.argv[1]
    inputFilePath = sys.argv[2]
    resultFilePath = sys.argv[3]

    ecs_infor_array = read_lines(ecsDataPath)
    input_file_array = read_lines(inputFilePath)

    # implementation the function predictVm
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)  #调用预测函数，返回结果
    print predic_result  #打印预测的结果
    # write the result to output file
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print 'main function end.'


def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\r\n" % item)
        # for item in array:
        #     output_file.write("%s\n" % item)
            # output_file.write('\r')
            # output_file.write(item)


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


if __name__ == "__main__":
    main()
