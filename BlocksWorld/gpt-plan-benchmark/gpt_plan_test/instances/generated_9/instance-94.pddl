

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a f)
(on b g)
(on c h)
(on d b)
(on e a)
(ontable f)
(on g c)
(on h i)
(on i e)
(clear d)
)
(:goal
(and
(on a c)
(on b i)
(on d g)
(on e f)
(on g h)
(on h a)
(on i d))
)
)


