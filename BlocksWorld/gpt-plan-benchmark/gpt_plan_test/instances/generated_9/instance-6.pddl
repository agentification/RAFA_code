

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b g)
(ontable c)
(on d c)
(on e i)
(on f b)
(on g a)
(ontable h)
(ontable i)
(clear d)
(clear f)
(clear h)
)
(:goal
(and
(on b c)
(on c g)
(on d a)
(on e d)
(on g f)
(on i h))
)
)


