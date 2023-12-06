

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b h)
(ontable c)
(ontable d)
(ontable e)
(on f i)
(ontable g)
(on h g)
(on i a)
(clear c)
(clear d)
(clear e)
(clear f)
)
(:goal
(and
(on a h)
(on c d)
(on d a)
(on e f)
(on f i)
(on g b)
(on i g))
)
)


