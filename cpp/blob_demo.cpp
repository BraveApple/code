#include <iostream>
#include <vector>
#include <caffe/blob.hpp>
#include <caffe/util/io.hpp>

using namespace std;
using namespace caffe;

int main() {
    Blob<float> a;
    cout << "Size: " << a.shape_string() << endl;
    a.Reshape(1, 2, 3, 4);
    cout << "Size: " << a.shape_string() << endl;

    float* p = a.mutable_cpu_data();
    float* q = a.mutable_cpu_diff();
    for(int i = 0; i < a.count(); i++) {
        p[i] = i; // 将data初始化为1, 2, 3 ...
        q[i] = a.count() - i - 1; // 将diff初始化为23, 22, 21 ...
    }

    a.Update(); // 实现dada与diff融合，即data = data - diff，也就是CNN权值更新步骤

    for(int n = 0; n < a.num(); n++) {
        for (int c = 0; c < a.channels(); c++) {
            for(int h = 0; h < a.height(); h++) {
                for(int w = 0; w < a.width(); w++) {
                    cout << "a[" << n <<"][" << c << "][" << h << "][" << w << "] = " << a.data_at(n, c, h, w) << endl; 
                }
            }
        }
    }
   
    cout << "ASUM = " << a.asum_data() << endl; // 计算所有元素的绝对值之和
    cout << "SUMSQ = " << a.sumsq_data() << endl; // 计算所有元素的平方和
    
    BlobProto bp1; // 构造一个BlobProto对象
    a.ToProto(&bp1, true); // 将a序列化，连同diff（默认不带）
    WriteProtoToBinaryFile(bp1, "a.blob"); // 写入磁盘文件"a.blob"
    BlobProto bp2; // 构造新的BlobProto对象
    ReadProtoFromBinaryFileOrDie("a.blob", &bp2); // 读取磁盘文件
    Blob<float> b; // 新建一个Blob对象
    b.FromProto(bp2, true); // 从序列化对象bp2中克隆b（连同形状）

    for(int n = 0; n < a.num(); n++) {
        for (int c = 0; c < a.channels(); c++) {
            for(int h = 0; h < a.height(); h++) {
                for(int w = 0; w < a.width(); w++) {
                    cout << "b[" << n <<"][" << c << "][" << h << "][" << w << "] = " << b.data_at(n, c, h, w) << endl; 
                }
            }
        }
    }

    return 0; 
}
