

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b d)
(ontable c)
(on d e)
(on e g)
(on f b)
(ontable g)
(on h a)
(on i f)
(clear h)
(clear i)
)
(:goal
(and
(on a f)
(on b h)
(on d c)
(on e g)
(on g i)
(on h d)
(on i a))
)
)


