

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b h)
(ontable c)
(on d a)
(on e g)
(on f c)
(ontable g)
(on h i)
(on i f)
(clear b)
(clear d)
)
(:goal
(and
(on b d)
(on d a)
(on e f)
(on g h)
(on h i)
(on i e))
)
)


