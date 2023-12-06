

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b f)
(on c i)
(on d h)
(on e g)
(ontable f)
(ontable g)
(on h a)
(on i d)
(clear c)
(clear e)
)
(:goal
(and
(on a h)
(on b f)
(on d i)
(on e d)
(on f a)
(on g e))
)
)


