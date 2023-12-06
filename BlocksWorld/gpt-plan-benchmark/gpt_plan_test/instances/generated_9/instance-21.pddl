

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b d)
(ontable c)
(on d a)
(on e i)
(on f c)
(on g b)
(ontable h)
(on i g)
(clear e)
(clear f)
)
(:goal
(and
(on a h)
(on b e)
(on c d)
(on e i)
(on i g))
)
)


