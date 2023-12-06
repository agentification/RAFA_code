

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b c)
(on c g)
(ontable d)
(on e a)
(ontable f)
(on g i)
(ontable h)
(on i e)
(clear b)
(clear d)
(clear f)
)
(:goal
(and
(on a f)
(on d b)
(on e g)
(on f h)
(on g d)
(on h c)
(on i a))
)
)


