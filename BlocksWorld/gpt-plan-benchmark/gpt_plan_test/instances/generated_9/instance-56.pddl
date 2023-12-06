

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c e)
(on d b)
(ontable e)
(on f a)
(on g f)
(ontable h)
(on i g)
(clear c)
(clear d)
(clear h)
(clear i)
)
(:goal
(and
(on b d)
(on g h)
(on h e)
(on i b))
)
)


