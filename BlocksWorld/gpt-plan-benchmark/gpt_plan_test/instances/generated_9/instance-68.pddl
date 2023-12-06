

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(on d f)
(on e i)
(ontable f)
(on g h)
(on h d)
(ontable i)
(clear a)
(clear b)
(clear e)
(clear g)
)
(:goal
(and
(on b i)
(on c a)
(on d h)
(on e g)
(on g b)
(on h f)
(on i d))
)
)


