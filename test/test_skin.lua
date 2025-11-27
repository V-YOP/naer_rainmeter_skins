function inc_after_ten_tick()
    for i = 1, 10 do
        cm.next_tick()
    end
    counter = counter + 1
end

function on_click()
    print('on_click')
    cm:append(coroutine.create(inc_after_ten_tick))
end

function Initialize()
    CoroutineManager = loadfile(SKIN:MakePathAbsolute('../CoroutineManager.lua'))()
    cm = CoroutineManager()
    counter = 0
end

function Update()
    cm:do_tick()
end