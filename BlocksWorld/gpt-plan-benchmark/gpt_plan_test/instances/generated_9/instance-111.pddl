

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c d)
(ontable d)
(on e b)
(on f c)
(on g a)
(on h i)
(on i e)
(clear g)
(clear h)
)
(:goal
(and
(on a i)
(on c h)
(on d b)
(on g e)
(on i g))
)
)


