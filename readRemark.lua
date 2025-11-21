
function readFile(filename)
    local file, err = io.open(filename, "r")
    if not file then
        return ""
    end
    
    local content = file:read("*a")
    file:close()
    return content or ""
end


function Initialize()
    remarkFilePath = SKIN:MakePathAbsolute('remark.txt')
end



function Update()
    return readFile(remarkFilePath)
end

