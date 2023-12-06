

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(ontable b)
(on c i)
(on d f)
(ontable e)
(on f c)
(on g a)
(ontable h)
(on i b)
(clear d)
(clear g)
(clear h)
)
(:goal
(and
(on a f)
(on d c)
(on g i)
(on h a)
(on i b))
)
)


