

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b c)
(on c a)
(on d h)
(on e i)
(on f d)
(on g f)
(ontable h)
(on i b)
(clear e)
(clear g)
)
(:goal
(and
(on a h)
(on b c)
(on c g)
(on e i)
(on f b)
(on i a))
)
)


