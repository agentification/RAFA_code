

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d g)
(on e i)
(on f b)
(on g h)
(on h a)
(on i c)
(clear d)
(clear e)
(clear f)
)
(:goal
(and
(on a d)
(on b h)
(on c a)
(on e b)
(on f c)
(on g f)
(on i g))
)
)


