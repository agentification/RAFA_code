

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b f)
(on c h)
(ontable d)
(ontable e)
(on f g)
(on g a)
(on h i)
(on i e)
(clear b)
(clear d)
)
(:goal
(and
(on b f)
(on c g)
(on e a)
(on f i)
(on g h)
(on h d)
(on i e))
)
)


