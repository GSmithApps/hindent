from composing import co
from library import wrap_in_unit_function, pri, p, our_id, concat


x = wrap_in_unit_function(1)
y = wrap_in_unit_function(2)
hey = wrap_in_unit_function("hey ")
there = wrap_in_unit_function("there")

z = co(
    pri,
    co(
        p,
        x,
        co(
            p,
            x,
            y
        ),
    )
)



co(
   co(pri,
      co(concat,
         hey,
         there)),
   co(pri,
      co(concat,
         hey,
         there)),
   co(pri,
      co(p,
         co(p,
            x,
            y),
         co(p,
            x,
            y))))