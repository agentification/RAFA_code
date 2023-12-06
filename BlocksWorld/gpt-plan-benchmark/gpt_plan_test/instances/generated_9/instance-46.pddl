

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c i)
(on d b)
(on e h)
(ontable f)
(on g a)
(on h f)
(on i e)
(clear c)
(clear d)
(clear g)
)
(:goal
(and
(on b h)
(on d f)
(on e d)
(on f c)
(on g i)
(on h a)
(on i e))
)
)


