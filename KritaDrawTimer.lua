
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

    counter = 0 
    -- 立即执行一次获取数据
    Update()
end

function roundToOneDecimal(num)
    return math.floor(num * 10 + 0.5) / 10  -- 四舍五入到1位小数
end

function setTodayCurrentTime(v)
    todayPercent = v / todayExpectTime
    todayPercentMulti100 = roundToOneDecimal(todayPercent * 100)
    todayCurrentTime = roundToOneDecimal(v)
end

function setWeekCurrentTime(v)
    weekPercent= v / weekExpectTime
    weekPercentMulti100= roundToOneDecimal(weekPercent * 100)
    weekCurrentTime = roundToOneDecimal(v)
end

function setMonthCurrentTime(v)
    monthPercent= v / monthExpectTime
    monthPercentMulti100= roundToOneDecimal(monthPercent * 100)
    monthCurrentTime = roundToOneDecimal(v)
end

function Update()
    -- 执行python的更新脚本
    if counter % 60 == 0 then
        print('BANG!')
        SKIN:Bang('!CommandMeasure', 'MeasureScript', 'Run')
    end
    counter = counter + 1
    local response = json.decode(SKIN:GetMeasure('MeasureScript'):GetStringValue())
    setTodayCurrentTime(response['today'] / 3600)
    setWeekCurrentTime(response['week'] / 3600)
    setMonthCurrentTime(response['month'] / 3600)
    -- 调用 Python 脚本并获取输出
    -- local command = 'python "' .. SKIN:GetVariable('CURRENTPATH') .. 'painting_time.py"'
    -- print(os.execute)
    -- local handle = io.popen(command)
    
    -- if handle then
    --     local result = handle:read("*a")
    --     handle:close()
        
    --     -- 解析输出 (格式: "0.3 2.0")
    --     if result and result ~= "" then
    --         local values = {}
    --         for value in string.gmatch(result, "%S+") do
    --             table.insert(values, value)
    --         end
            
    --         if #values >= 2 then
    --             currentTime = values[1]
    --             expectTime = values[2]
    --         end
    --     end
    -- end
end

