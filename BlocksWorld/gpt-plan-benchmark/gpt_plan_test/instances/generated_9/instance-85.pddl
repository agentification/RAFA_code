

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c h)
(on d f)
(ontable e)
(on f g)
(on g c)
(on h a)
(on i b)
(clear d)
(clear e)
(clear i)
)
(:goal
(and
(on a b)
(on d g)
(on f a)
(on g c)
(on i d))
)
)


