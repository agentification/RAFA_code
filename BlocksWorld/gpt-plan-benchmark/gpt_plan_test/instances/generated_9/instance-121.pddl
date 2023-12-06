

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b e)
(on c b)
(ontable d)
(on e g)
(on f h)
(on g f)
(ontable h)
(ontable i)
(clear a)
(clear d)
(clear i)
)
(:goal
(and
(on a e)
(on c g)
(on d f)
(on e d)
(on g i)
(on i a))
)
)


