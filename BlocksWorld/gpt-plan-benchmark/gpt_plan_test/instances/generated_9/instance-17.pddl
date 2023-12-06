

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b i)
(on c d)
(ontable d)
(on e f)
(ontable f)
(on g c)
(ontable h)
(on i g)
(clear a)
(clear e)
(clear h)
)
(:goal
(and
(on a h)
(on b c)
(on c a)
(on d e)
(on e i)
(on g d)
(on i b))
)
)


