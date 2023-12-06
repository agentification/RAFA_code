

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b g)
(on c d)
(ontable d)
(ontable e)
(on f b)
(ontable g)
(on h a)
(ontable i)
(clear c)
(clear f)
(clear h)
(clear i)
)
(:goal
(and
(on a c)
(on b f)
(on d i)
(on e a)
(on f h)
(on g d)
(on h g)
(on i e))
)
)


