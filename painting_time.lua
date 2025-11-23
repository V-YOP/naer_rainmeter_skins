
function Initialize()
    json = loadfile(SKIN:MakePathAbsolute('dkjson.lua'))()
    -- 初始化变量
    -- TODO 把 expect 挪到 variable
    -- 但 tm 怎么可能会有这种必要？

    todayCurrentTime = 0
    todayExpectTime = 2
    todayPercent = 0
    todayPercentMulti100 = 0
    
    weekCurrentTime = 0
    weekExpectTime = 20
    weekPercent = 0
    weekPercentMulti100 = 0
    
    monthCurrentTime = 0
    monthExpectTime = 80
    monthPercent = 0
    monthPercentMulti100 = 0

    current_combo = 0
    thirtyMinsBeforeTime = 0
    delta_to_last_drawtime = ''

    counter = 0 
    -- 立即执行一次获取数据
    Update()
end

function roundToOneDecimal(num)
    return math.floor(num * 10 + 0.5) / 10  -- 四舍五入到1位小数
end

function getTimeDifference(timeStr)
    -- 计算给定日期和当前日期的时间差并使用 HH:MM:SS 去表示
    local y, m, d, H, M, S = timeStr:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
    local diff = os.time() - os.time({year=y, month=m, day=d, hour=H, min=M, sec=S})
    
    local h = math.floor(diff / 3600)
    local m = math.floor((diff % 3600) / 60)
    local s = diff % 60
    
    return string.format("%02d:%02d:%02d", h, m, s)
end


function setTodayCurrentTime(v)
    todayPercent = v / todayExpectTime
    todayPercentMulti100 = roundToOneDecimal(todayPercent * 100)
    todayCurrentTime = roundToOneDecimal(v)
end

function setWeekCurrentTime(v)
    weekPercent= v / weekExpectTime
    weekPercentMulti100 = roundToOneDecimal(weekPercent * 100)
    weekCurrentTime = roundToOneDecimal(v)
end

function setMonthCurrentTime(v)
    monthPercent= v / monthExpectTime
    monthPercentMulti100 = roundToOneDecimal(monthPercent * 100)
    monthCurrentTime = roundToOneDecimal(v)
end

function Update()
    -- 执行python的更新脚本
    if counter % 60 == 0 then
        print('BANG!')
        -- 这个run是不阻塞的！
        SKIN:Bang('!CommandMeasure', 'MeasurePaintingTimeScript', 'Run')
    end
    counter = counter + 1
    local response = json.decode(SKIN:GetMeasure('MeasurePaintingTimeScript'):GetStringValue())
    if not response then 
        return 
    end
    delta_to_last_drawtime = getTimeDifference(response['latest_drawtime'])
    thirtyMinsBeforeTime = response['30_mins_before'] / 1500 -- 半小时的窗口，最大值是 1800 秒，但这里松一些，1500 秒就是1
    current_combo = response['current_combo']
    
    setTodayCurrentTime(response['today'] / 3600)
    setWeekCurrentTime(response['week'] / 3600)
    setMonthCurrentTime(response['month'] / 3600)
end

