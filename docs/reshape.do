// Reshapes exported data from signalbox 
// Saves file called `out'.data which has one row per ob


local in = "~/Downloads/2010-11-15 11-56-14.902218-Users-ben-Django-signals-tmp-some.csv"
local out = "myfile"

clear 
insheet using "`in'", tab names
sort user observation created
drop row_id last_modified created
reshape wide answer@, i(observation) j(variable_name) string
renpfix answer              
destring *, replace
sencode user, gen(person)
sencode observation, gen(ob)
desc, f
list, nolab

save `out', replace