

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(on c i)
(on d e)
(ontable e)
(on f c)
(on g a)
(on h d)
(on i h)
(clear b)
(clear f)
)
(:goal
(and
(on c h)
(on d c)
(on e b)
(on f a)
(on h g)
(on i f))
)
)


