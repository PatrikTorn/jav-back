"""
IDataType = {
    x: Float,
    y: Float,
    z: Float
}
GyroData = {
    ArrayGyro: IDataType[],
    Timestamp: 89675348
}
AccData = {
    ArrayAcc: IDataType[],
    Timestamp: 89675348
}
@param calib_data: {
    accMeasures: AccData[],
    gyroMeasures: GyroData[]
}
@param throw_data: {
    accMeasures: AccData[],
    gyroMeasures: GyroData[]
}
@param *_ts: Integer
@return velocity: Float
@return angle: Float
"""
def calculate(
    calib_data,
    throw_data,
    start_ts,
    end_ts,
    calib_start_ts,
    calib_end_ts
):
    # Do something with raw data

    return {
        'velocity': 26.23,
        'angle': 34.664
    }
