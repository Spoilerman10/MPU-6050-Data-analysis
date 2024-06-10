# MPU-6050-Data-analysis
Programming project - Roll, pitch, yaw angles IMU MPU6050.

In this code the roll, pitch and yaw angles are measured with the accelerometer and gyroscope of IMU MPU6050 and Arduino UNO.

The library used for the MPU6050 was "Simple MPU6050" https://github.com/ZHomeSlice/Simple_MPU6050 The porpouse was obtain the acceleration and angular velocity.

File complementary filter: The roll, pitch and yaw angles are calculate with the acceleration and angular velocity. And then the complementary filter is implemented to obtain the final angle values. The main source was https://www.luisllamas.es/medir-la-inclinacion-imu-arduino-filtro-complementario/

Finally the graphics of angles are shown.

Acording to the datasheet and library used the Sensitivity Scale for the gycope is 16.4 LSB/(º/s) and for the accelerometer is 2,048 LSB/g.

MPU datasheet: https://pdf1.alldatasheet.com/datasheet-pdf/download/517744/ETC1/MPU-6050.html 
