

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b h)
(ontable c)
(on d i)
(on e g)
(on f e)
(on g a)
(ontable h)
(on i c)
(clear d)
(clear f)
)
(:goal
(and
(on a d)
(on b i)
(on c h)
(on d b)
(on e c)
(on i f))
)
)


