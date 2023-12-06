

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b d)
(on c a)
(ontable d)
(on e i)
(ontable f)
(on g f)
(on h c)
(ontable i)
(clear e)
(clear g)
(clear h)
)
(:goal
(and
(on c h)
(on d b)
(on e f)
(on h i)
(on i g))
)
)


