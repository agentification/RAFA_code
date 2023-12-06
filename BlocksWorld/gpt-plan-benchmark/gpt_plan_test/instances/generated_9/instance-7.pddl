

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c i)
(on d c)
(on e d)
(on f b)
(on g f)
(ontable h)
(on i g)
(clear a)
(clear e)
(clear h)
)
(:goal
(and
(on a d)
(on b c)
(on c h)
(on d f)
(on e b)
(on f g)
(on g e)
(on i a))
)
)


