local NEXT_TICK_LABEL = {}

local function index_of(list, v)
    for i, value in pairs(list) do
        if value == v then
            return i
        end
    end
end

function CoroutineManager()
    local next_tick_threads = {} -- 待resume的协程们
    local function resume_thread(co)
        if coroutine.status(co) == 'dead' then
            next_tick_threads[co] = nil
            return
        end

        local success, v = coroutine.resume(co)
        if not success then
            -- TODO
        end
        if v == NEXT_TICK_LABEL and not index_of(next_tick_threads, co) then
            next_tick_threads[co] = co
        end
    end
    return {
        ---@async
        next_tick = function(self)
            -- wait until next_tick
            coroutine.yield(NEXT_TICK_LABEL)
        end,
        wait_until = function(self, p)
            while true do
                if p then return end
                coroutine.yield(NEXT_TICK_LABEL)
            end
        end,
        append = function (self, co)
            next_tick_threads[co] = co
        end,
        do_tick = function(self)
            for _, v in pairs(next_tick_threads) do
                resume_thread(v)
            end
        end
    } 
end

return CoroutineManager
