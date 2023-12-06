

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b g)
(on c d)
(on d b)
(on e c)
(ontable f)
(on g h)
(ontable h)
(on i a)
(clear f)
(clear i)
)
(:goal
(and
(on a b)
(on b i)
(on d c)
(on e g)
(on f e)
(on g a)
(on h f)
(on i d))
)
)


